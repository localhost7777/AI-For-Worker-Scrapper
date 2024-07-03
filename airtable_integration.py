from pyairtable import Api
import os


class AirtableIntegration:
    def __init__(self, base_id=None, api_key=None):
        self.base_id = base_id
        self.api_key = api_key


    # Base API connection with airtable
    def connect(self):
        return Api(self.api_key)
        # print(self.api_key)
        # return Base(api_key=self.api_key, base_id=self.base_id)

    
    def publish(self, data, table_id, identifier):
        api = self.connect()
        table = api.table(self.base_id, table_id)
        records = table.all() # Get all the data in requested table
        
        # update airtable
        record_exists = False
        try:
            for record in records:
                try:
                    # check if the data already exist in airtable
                    if data.get(identifier) == record['fields'][identifier]:
                        print(f"Updating Existing Data : {table_name} - {data.get(identifier)}")
                        table.update( record['id'], data)
                        record_exists = True
                        break
                except Exception as e:
                    print(f"error occurred: {table_name} - {data.get(identifier)} {e}")

            try:
                if not record_exists:
                    print(f"Creating New Data : {table_name} - {data.get(identifier)}")
                    # table.create(table_name, data, typecast=True)
                    table.create(data)
            except Exception as e:
                print(f"error occurred: {table_name} - {data.get(identifier)} {e}")
        except Exception as e:
            print("provided data cannot be added to the field in airtable : ", e)