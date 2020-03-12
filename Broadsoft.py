import requests
import xmltodict
import collections

from datetime import datetime
from requests.auth import HTTPBasicAuth

"""
TODO:
/v2.0/user/<userid>/directories/CallLogs
/v2.0/user/<userid>/directories/CallLogs/Missed/<callLogId>
/v2.0/user/<userid>/directories/CallLogs/Placed/<callLogId>
/v2.0/user/<userid>/directories/CallLogs/Received/<callLogId>
/v2.0/user/<userid>/directories/CustomContact
/v2.0/user/<userid>/directories/CustomContact/<directoryName>
/v2.0/user/<userid>/directories/EnhancedCallLogs
/v2.0/user/<userid>/directories/EnhancedCallLogs/Missed
/v2.0/user/<userid>/directories/EnhancedCallLogs/Missed/<callLogId>
/v2.0/user/<userid>/directories/EnhancedCallLogs/Placed
/v2.0/user/<userid>/directories/EnhancedCallLogs/Placed/<callLogId>
/v2.0/user/<userid>/directories/EnhancedCallLogs/Received
/v2.0/user/<userid>/directories/EnhancedCallLogs/Received/<callLogId>
/v2.0/user/<userid>/directories/FlexibleSeatingHosts
/v2.0/user/<userid>/directories/HotelingHosts

DONE:
/v2.0/user/<userid>/directories/CallLogs/Missed
/v2.0/user/<userid>/directories/CallLogs/Placed
/v2.0/user/<userid>/directories/CallLogs/Received
/v2.0/user/<userid>/directories/Enterprise
/v2.0/user/<userid>/directories/EnterpriseCommon
/v2.0/user/<userid>/directories/Group
/v2.0/user/<userid>/directories/GroupCommon
/v2.0/user/<userid>/directories/Personal


"""


class XSI:
    """
        Based on:
        Cisco BroadWorks Xtended Services Interface Interface Specification
        Release 23.0 Document Version 3
        Link:
        https://pubhub.devnetcloud.com/media/broadsoft-docs/docs/pdf/BW-XSIInterfaceSpec-R230.pdf
    """

    def __init__(self,bw_user:str, bw_password:str, host='https://client.deutschland-lan.de'):
        self.bw_user = bw_user
        self.bw_password = bw_password
        self.xsi_url = host + '/com.broadsoft.xsi-actions/v2.0/user'
        self.headers = {'user-agent': 'XSI-Client/0.0.1', 'Content-type': 'application/xml; charset=UTF-8'}

    def __doc__(self):
        return \
            "Cisco BroadWorks Xtended Services Interface Interface Specification" \
            "Release 23.0 Document Version 3"

    def __build_url(self, action, user=None) -> str:
        if user is None:
            user = self.bw_user
        return self.xsi_url + '/' + user + action

    def __get(self,action, params=None) -> dict:
        response = requests.get(self.__build_url(action), params=params, auth=HTTPBasicAuth(username=self.bw_user, password=self.bw_password))
        if response.status_code==200:
            return xmltodict.parse(response.text)
        else:
            return None


    def profile(self) -> dict:
        #TODO: Actual only a placeholder
        XSI_COMMAND = '/Profile'
        return self.__get(XSI_COMMAND)


    def directories_personal(self, start=1, step=50) -> dict:

        def identify_total_records(action):
            xsi_response = self.__get(action, {'start': 1, 'numberOfRecords': 1})
            return int(xsi_response['Personal']['totalAvailableRecords'])

        XSI_COMMAND = '/directories/Personal'

        directory = []
        max = identify_total_records (XSI_COMMAND)

        if max >0 :
            for i in range(start, max, step):
                for directory_item in self.__get(XSI_COMMAND, {'start': i})['Personal']['commonPhoneEntry']:
                    keys=list(directory_item.keys())
                    values=list(directory_item.values())

                    directory.append(
                        dict( zip(keys,values)))

        return directory



    def directories_group_common(self, start=1, step=50) -> dict:

        def identify_total_records(action):
            xsi_response = self.__get(action, {'start': 1, 'numberOfRecords': 1})
            return int(xsi_response['GroupCommon']['totalAvailableRecords'])

        XSI_COMMAND = '/directories/GroupCommon'

        directory = []
        max = identify_total_records (XSI_COMMAND)

        if max >0 :
            for i in range(start, max, step):
                for directory_item in self.__get(XSI_COMMAND, {'start': i})['GroupCommon']['commonPhoneEntry']:
                    keys=list(directory_item.keys())
                    values=list(directory_item.values())

                    directory.append(
                        dict( zip(keys,values)))

        return directory


    def directories_enterprise_common(self, start=1, step=50) -> dict:
        """
        This service allows the retrieval of a user’s enterprise common phone list for a user.

        :param start: This is the starting result position to return. The default value is “1”.
        :param step: This is the number of results to return per page.
        :return: list of dicts with name and number
        :rtype: dict
        """
        def identify_total_records(action):
            xsi_response = self.__get(action, {'start': 1, 'numberOfRecords': 1})
            return int(xsi_response['EnterpriseCommon']['totalAvailableRecords'])

        XSI_COMMAND = '/directories/EnterpriseCommon'

        directory = []
        max = identify_total_records (XSI_COMMAND)

        if max >0 :
            for i in range(start, max, step):
                for directory_item in self.__get(XSI_COMMAND, {'start': i})['EnterpriseCommon']['commonPhoneEntry']:
                    keys=list(directory_item.keys())
                    values=list(directory_item.values())

                    directory.append(
                        dict( zip(keys,values)))

        return directory

    def directories_enterprise(self, start=1, step=50, hirangana=0) -> dict:

        def identify_total_records(action):
            xsi_response = self.__get(action, {'start': 1, 'numberOfRecords': 1})
            return int(xsi_response['Enterprise']['totalAvailableRecords'])

        XSI_COMMAND = '/directories/Enterprise'
        directory = []

        max = identify_total_records(XSI_COMMAND)

        if max > 0:
            for i in range(start, max, step):
                for directory_item in self.__get(XSI_COMMAND, {'start':i})['Enterprise']['enterpriseDirectory']['directoryDetails']:

                    # integrate sub-directories
                    for value in list(directory_item.values()):
                        if isinstance(value , collections.OrderedDict):
                            directory_item.update(value)

                            # TODO: eliminate quick & dirty method
                            del directory_item['additionalDetails']

                            if not hirangana:
                                del directory_item['hiranganaLastName']
                                del directory_item['hiranganaFirstName']

                    keys = list(directory_item.keys())
                    values = list(directory_item.values())

                    directory.append(dict(zip(keys, values)))
        return directory


    def directories_group(self, start=1, step=50, hirangana=0) -> dict:

        def identify_total_records(action):
            xsi_response = self.__get(action, {'start': 1, 'numberOfRecords': 1})
            return int(xsi_response['Group']['totalAvailableRecords'])

        XSI_COMMAND = '/directories/Group'
        directory = []

        max = identify_total_records(XSI_COMMAND)

        if max > 0:
            for i in range(start, max, step):
                for directory_item in self.__get(XSI_COMMAND, {'start':i})['Group']['groupDirectory']['directoryDetails']:

                    # integrate sub-directories
                    for value in list(directory_item.values()):
                        if isinstance(value , collections.OrderedDict):
                            directory_item.update(value)

                            # TODO: eliminate quick & dirty method
                            del directory_item['additionalDetails']

                            if not hirangana:
                                del directory_item['hiranganaLastName']
                                del directory_item['hiranganaFirstName']

                    keys = list(directory_item.keys())
                    values = list(directory_item.values())

                    directory.append(dict(zip(keys, values)))
        return directory



    def directories_call_logs_missed(self) -> dict:
        XSI_COMMAND = '/directories/CallLogs/Missed'
        directory = []


        for item in self.__get(XSI_COMMAND)['missed']['callLogsEntry']:
            if item['name']=='Unavailable':
                item['name']=None

            item['time'] = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S.%f%z')

            keys=list(item.keys())
            values=list(item.values())

            directory.append(
                dict( zip(keys, values)))

        return directory


    def directories_call_logs_placed(self) -> dict:
        XSI_COMMAND = '/directories/CallLogs/Placed'
        directory = []


        for item in self.__get(XSI_COMMAND)['placed']['callLogsEntry']:
            if item['name']=='Unavailable':
                item['name']=None

            item['time'] = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S.%f%z')

            keys=list(item.keys())
            values=list(item.values())

            directory.append(
                dict( zip(keys, values)))

        return directory

    def directories_call_logs_received(self) -> dict:
        XSI_COMMAND = '/directories/CallLogs/Received'
        directory = []


        for item in self.__get(XSI_COMMAND)['received']['callLogsEntry']:
            if item['name']=='Unavailable':
                item['name']=None

            item['time'] = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S.%f%z')

            keys=list(item.keys())
            values=list(item.values())

            directory.append(
                dict( zip(keys, values)))

        return directory
"""
Received 
"""

