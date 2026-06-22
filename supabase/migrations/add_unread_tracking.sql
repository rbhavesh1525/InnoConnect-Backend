-- Migration: add messages and collaboration_requests tables with unread tracking
-- Run in Supabase SQL Editor if tables do not exist yet

create table if not exists messages (
  id bigint generated always as identity primary key,
  sender_id uuid not null references users(user_id) on delete cascade,
  receiver_id uuid not null references users(user_id) on delete cascade,
  message text not null,
  is_read boolean not null default false,
  created_at timestamptz default now()
);

create index if not exists idx_messages_receiver_unread
  on messages (receiver_id, is_read)
  where is_read = false;

create table if not exists collaboration_requests (
  request_id bigint generated always as identity primary key,
  sender_id uuid not null references users(user_id) on delete cascade,
  receiver_id uuid not null references users(user_id) on delete cascade,
  project_id bigint not null references projects(id) on delete cascade,
  status text not null default 'pending',
  created_at timestamptz default now()
);

-- If messages table already exists without is_read, run:
-- alter table messages add column if not exists is_read boolean not null default false;
