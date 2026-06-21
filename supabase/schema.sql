-- Run this in the Supabase SQL Editor

create extension if not exists vector;

create table if not exists users (
  user_id uuid primary key,
  name text not null,
  email text not null unique,
  interests text[] not null
);

create table if not exists projects (
  id bigint generated always as identity primary key,
  owner text,
  owner_id uuid references users(user_id) on delete set null,
  project_title text not null,
  description text,
  problem_statement text,
  solution_overview text,
  industry_category text,
  created_at timestamptz default now()
);

create table if not exists project_embeddings (
  project_id bigint primary key references projects(id) on delete cascade,
  embedding vector(768)
);
