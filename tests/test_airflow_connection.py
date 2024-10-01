from airflow.hooks.base import BaseHook

def test_connection():
    try:
        conn = BaseHook.get_connection('house_prices')
        print(f"Host: {conn.host}")
        print(f"Schema: {conn.schema}")
        print(f"Login: {conn.login}")
        print(f"Password: {conn.password}")
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()