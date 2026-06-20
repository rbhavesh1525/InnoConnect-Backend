-- Run this in the Supabase SQL Editor if projects already exists without owner_id

alter table projects
  add column if not exists owner_id uuid references users(user_id) on delete set null;
