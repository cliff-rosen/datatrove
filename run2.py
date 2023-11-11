import gsheets as gs

SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'

print(gs.creds)
gs.google_auth()
print(gs.creds)
sheet = gs.get_sheet(SPREADSHEET_ID)
