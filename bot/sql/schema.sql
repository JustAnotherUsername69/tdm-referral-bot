CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT PRIMARY KEY,
  username TEXT,
  first_seen TIMESTAMP,
  referred_by BIGINT,
  referrals INTEGER DEFAULT 0,
  points INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS coupons (
  id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  used_by BIGINT,
  used_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coupon_history (
  id SERIAL PRIMARY KEY,
  user_id BIGINT,
  code TEXT,
  redeemed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS broadcasts (
  id SERIAL PRIMARY KEY,
  admin_id BIGINT,
  payload_type TEXT,
  payload_text TEXT,
  payload_file_id TEXT,
  created_at TIMESTAMP DEFAULT now(),
  status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS broadcast_recipients (
  id SERIAL PRIMARY KEY,
  broadcast_id INT REFERENCES broadcasts(id) ON DELETE CASCADE,
  user_id BIGINT,
  status TEXT DEFAULT 'pending',
  error TEXT
);
