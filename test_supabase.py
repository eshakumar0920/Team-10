from config import Config

def test_supabase_connection():
    try:
        response = Config.SUPABASE_CLIENT.auth.sign_in_with_password({"email" : "test@example.com", "password" : "testpassword"})
       # print("Supabase connection successful:", response)
        print("Supabase connection successful:")
    except Exception as e:
        print("Error connecting to Supabase:", e)


if __name__ == '__main__':
    test_supabase_connection()