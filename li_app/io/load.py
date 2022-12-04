from abc import ABC, abstractmethod

import boto3
import streamlit as st

class LoadUnstructured(ABC):
    @abstractmethod
    def get(self):
        pass


class DynamoDBLoader(LoadUnstructured):
    '''
    Fetches table from DynamoDB using Boto.
    Needs to have authentication set up through env variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY 
    '''
    def __init__(
        self,
        table: str,
        attributes: list
    ):
        self.db = boto3.resource('dynamodb')
        self.table = db.Table('LinkedInDSJobs')
        self.attributes = attributes #['job_id','date','title']

    @st.cache
    def get(self, date):
        data = self.scanRecursive(
            dbTable=table,
            Select='SPECIFIC_ATTRIBUTES',
            AttributesToGet=attributes) 
            # I'm using default value for Select option
            # I could extend the interface by passing kwargs to scanRecursive, 
            # but atm it would introduce unnecessary complexity in the interface 
            
        data_df = pd.DataFrame(data) # This will give error if structure is not consistent    
        return data_df
        

    @staticmethod
    def scanRecursive(dbTable, **kwargs):
        """
        NOTE: Anytime you are filtering by a specific equivalency attribute such as id, name 
        or date equal to ... etc., you should consider using a query not scan

        kwargs are any parameters you want to pass to the scan operation

        Taken from: 
        """
        response = dbTable.scan(**kwargs)
        if kwargs.get('Select')=="COUNT":
            return response.get('Count')
        data = response.get('Items')
        while 'LastEvaluatedKey' in response:
            response = kwargs.get('table').scan(ExclusiveStartKey=response['LastEvaluatedKey'], **kwargs)
            data.extend(response['Items'])
        return data