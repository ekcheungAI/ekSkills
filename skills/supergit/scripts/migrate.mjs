#!/usr/bin/env node
// supergit migrate — apply ONE database migration file the ledger-correct way.
//
//   - the file's own timestamp becomes the ledger version (never a fresh one)
//   - the DDL and the ledger row commit in ONE transaction; the ledger stores
//     the full file text, so a later audit can diff repo vs. database exactly
//   - refuses if that version is already in the ledger
//   - --check  runs the file inside a transaction and rolls it back (syntax +
//              semantics proven against production, nothing changed)
//   - --dry-run only reports what would happen
//
// Usage:
//   node migrate.mjs <path/to/YYYYMMDDHHMMSS_name.sql> [--check | --dry-run]
//
// Connection: DATABASE_URL (a postgres:// URL). If unset, the script reads
// .env.local / .env in the current directory for DATABASE_URL, or for the
// Supabase shape SUPABASE_DB_HOST / SUPABASE_DB_USER / SUPABASE_DB_PASSWORD.
// The `pg` package is resolved from the project you run this in.
//
// Ledger: supabase_migrations.schema_migrations(version, name, statements) —
// the table the Supabase CLI and dashboard also read. Override with
// MIGRATION_LEDGER=schema.table if your project keeps it elsewhere.
import { readFileSync, existsSync } from "node:fs";
import { basename, join } from "node:path";
import { createRequire } from "node:module";

const file = process.argv[2];
const check = process.argv.includes("--check");
const dry = process.argv.includes("--dry-run");
if (!file) { console.error("usage: migrate.mjs <YYYYMMDDHHMMSS_name.sql> [--check|--dry-run]"); process.exit(1); }
const m = basename(file).match(/^(\d{14})_(.+)\.sql$/);
if (!m) { console.error("filename must be YYYYMMDDHHMMSS_name.sql — the timestamp IS the ledger version"); process.exit(1); }
const [, version, name] = m;
const sql = readFileSync(file, "utf8");

function envFile() {
  const out = {};
  for (const f of [".env.local", ".env"]) {
    const p = join(process.cwd(), f);
    if (!existsSync(p)) continue;
    for (const line of readFileSync(p, "utf8").split("\n")) {
      if (!line.includes("=") || line.trim().startsWith("#")) continue;
      const i = line.indexOf("=");
      out[line.slice(0, i).trim()] ??= line.slice(i + 1).trim().replace(/^"|"$/g, "");
    }
  }
  return out;
}
const env = { ...envFile(), ...process.env };
const ledger = env.MIGRATION_LEDGER || "supabase_migrations.schema_migrations";
if (!/^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)?$/i.test(ledger)) { console.error("MIGRATION_LEDGER must be schema.table"); process.exit(1); }

let conn;
if (env.DATABASE_URL) conn = { connectionString: env.DATABASE_URL, ssl: { rejectUnauthorized: false } };
else if (env.SUPABASE_DB_HOST && env.SUPABASE_DB_USER && env.SUPABASE_DB_PASSWORD)
  conn = { host: env.SUPABASE_DB_HOST, port: Number(env.SUPABASE_DB_PORT || 5432), user: env.SUPABASE_DB_USER,
           database: env.SUPABASE_DB_NAME || "postgres", password: env.SUPABASE_DB_PASSWORD, ssl: { rejectUnauthorized: false } };
else { console.error("no connection: set DATABASE_URL, or SUPABASE_DB_HOST/USER/PASSWORD (in the environment or .env.local)"); process.exit(1); }

const { Client } = createRequire(join(process.cwd(), "package.json"))("pg");
const c = new Client(conn);
await c.connect();
try {
  const exists = await c.query(`select 1 from ${ledger} where version=$1`, [version]);
  if (exists.rowCount) { console.log(`already in ledger: ${version} ${name} — nothing done`); process.exit(2); }
  if (dry) { console.log(`dry run: would apply ${version}_${name} (${sql.length} bytes) and write ledger row ${version}`); process.exit(0); }
  await c.query("begin");
  await c.query(sql);
  if (check) {
    await c.query("rollback");
    console.log(`CHECK OK — parsed and executed against the live schema, then rolled back: ${version} ${name}`);
    process.exit(0);
  }
  await c.query(`insert into ${ledger} (version, name, statements) values ($1, $2, array[$3])`, [version, name, sql]);
  await c.query("commit");
  console.log(`applied + ledgered: ${version} ${name} (${sql.length} bytes)`);
} catch (e) {
  await c.query("rollback").catch(() => {});
  console.error(`FAILED (rolled back, nothing changed): ${e.message}`);
  process.exit(1);
} finally { await c.end(); }
