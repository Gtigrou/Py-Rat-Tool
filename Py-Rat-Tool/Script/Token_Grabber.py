import sqlite3
import os

def get_histoy(browser_name:  str = "Edge"):
    for username in os.listdir(r"C:\Users"):
        if username not in ['All Users', 'Default', "Default User", "desktop.ini", "Public"]:
            path = rf'C:\Users\{username}\AppData\Local\Microsoft\{browser_name}\User Data\Default\History'
            print(f"Trying to access: {path}")

            if os.path.exists(path):
                try:

                    temp_path = rf"C:\Temp\{username}_History"
                    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                    with open(path, 'rb') as source, open(temp_path, 'wb') as target:
                        target.write(source.read())

                    db = sqlite3.connect(temp_path)
                    cursor = db.cursor()

                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    print(f"Tables found: {tables}")

                    if ('urls',) in tables:
                        cursor.execute("SELECT * FROM urls;")
                        final = []
                        for row in cursor.fetchall():
                            print(row)
                    else:
                        return "- No 'urls' table found in the database."

                    db.close()
                    os.remove(temp_path)
                except Exception as e:
                    return f"- Error while extracting History: {e}"
            else:
                return "- History file not found"

def test_all():
    testList = ["Edge", "Chrome", "Opera"]
    history = dict()
    for i in testList:
        history.update({i: get_histoy(i)})
    return history

if __name__ == '__main__':
    print(test_all())
