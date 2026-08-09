# Notion setup for Rukky's dashboard

## 1. Create the database
In Notion, create a new **Table** database (call it e.g. "Rukky UGC Trends") with these
properties — names must match the workflow exactly:

| Property name        | Type       | Notes                                              |
|----------------------|------------|----------------------------------------------------|
| `Topic`              | Title      | The trending topic (default title column)          |
| `Hooks`              | Text       | 3 AI hooks, newline-separated                       |
| `Strategy`           | Text       | Short AI campaign strategy                           |
| `Source Link`        | URL        | Where the trend came from                            |
| `Performance Status` | Select     | Options: `New`, `Tested`, `Failed`, `Viral`         |

`Performance Status` is the column the v2.0 feedback loop will read back into the LLM.

## 2. Connect Notion to n8n
1. Go to https://www.notion.so/my-integrations → **New integration** → copy the secret.
2. Open your database → **•••** menu → **Connections** → add your integration
   (n8n can't see the DB until you share it here — easy step to miss).
3. In n8n Cloud → **Credentials** → **New** → *Notion API* → paste the secret.
4. In the **Save To Notion Dashboard** node, pick the credential, then select the
   database from the list (this fills the real database ID, replacing the placeholder).

## 3. Get the database ID (if selecting from the list doesn't work)
The ID is the 32-char hash in the DB URL:
`https://notion.so/<workspace>/<THIS_IS_THE_DATABASE_ID>?v=...`
