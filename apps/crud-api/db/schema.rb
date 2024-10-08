# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.2].define(version: 2024_08_17_143820) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "payment_participants", force: :cascade do |t|
    t.uuid "payment_id", null: false
    t.uuid "user_id", null: false
    t.integer "weight", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["payment_id"], name: "index_payment_participants_on_payment_id"
    t.index ["user_id"], name: "index_payment_participants_on_user_id"
  end

  create_table "payments", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.uuid "settlement_session_id", null: false
    t.uuid "paid_by_id", null: false
    t.string "title", null: false
    t.text "description"
    t.integer "amount", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["paid_by_id"], name: "index_payments_on_paid_by_id"
    t.index ["settlement_session_id"], name: "index_payments_on_settlement_session_id"
  end

  create_table "settlement_session_participants", force: :cascade do |t|
    t.uuid "settlement_session_id", null: false
    t.uuid "user_id", null: false
    t.datetime "joined_at", null: false
    t.integer "role", null: false
    t.integer "settlement_status", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["settlement_session_id"], name: "index_settlement_session_participants_on_settlement_session_id"
    t.index ["user_id"], name: "index_settlement_session_participants_on_user_id"
  end

  create_table "settlement_sessions", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.string "title", null: false
    t.integer "visibility_scope", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "users", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_foreign_key "payment_participants", "payments"
  add_foreign_key "payment_participants", "users"
  add_foreign_key "payments", "settlement_sessions"
  add_foreign_key "payments", "users", column: "paid_by_id"
  add_foreign_key "settlement_session_participants", "settlement_sessions"
  add_foreign_key "settlement_session_participants", "users"
end
