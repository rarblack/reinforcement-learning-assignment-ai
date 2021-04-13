from exceptions import *
import requests
import sys


class Connection:

    def __init__(self, api_key, user_id):
        self.__url      = 'https://www.notexponential.com/aip2pgaming/api/rl/'
        self.__headers  = { 
                    'User-Agent'   :  'Terminal',
                    'Accept'       :  '*/*',
                    'x-api-key'    :  api_key, 
                    'userId'       :  user_id,
                    'Content-Type' : 'application/x-www-form-urlencoded', 
                }


    def __send_post_request(self, payload, url_ending = 'gw.php'):
        return requests.post(self.__url + url_ending, headers=self.__headers, data=payload)

    def __send_get_request(self, params, url_ending = 'gw.php'):
        return requests.get(self.__url + url_ending + '?' + params, headers=self.__headers, data={})

    def get_me_located(self):
        """
        Return Values: your current world and state in that world.  
        Think of this as your GPS, and confirm where you are.  
        If you are in world “-1”, that means you are in no world, and you can enter a world.
        
        This call is entirely optional and is useful only for debugging purposes.Your program does not need to make this call.
        """
        params = f'type=location&teamID={teamId}'
        response = self.__send_get_request(params)
        return self.__validate(response)

    def post_a_world(self, worldId, teamId):
        """
        Body: type=”enter”, worldId=$worldId, teamId=$teamId
        Return Values: The new $runId started
        Fails if you are already in a world.

        This is the starting part of your “learning” agent.
        Introduce a delay and do not make more than one enter call every 10 minutes.


        """
        payload = {
            'type': 'enter', 
            'worldId': worldId,
            'teamId': teamId
        }
        response = self.__send_post_request(payload)
        return self.__validate(response)

    def post_a_move(self, teamId, move):
        """
        Return Values: Reward, New State entered $runId started
        Fails if you are not already in a world (in that case, enter a world first).

        This is the central part of your “learning” agent.
        Your program needs to carefully process the result.
        Introduce a delay and do not make more than one move call every 15 seconds.
        """
        payload = {
            'type': 'move', 
            'teamId': teamId,
            'move': move,
        }

        response = self.__send_post_request(payload)
        return self.__validate(response)
    
    def get_my_teams_rl_score(self, teamId):
        """
        Return Values: score.  Fails if you are not in the team (you can only get scores for your team).
        
        This call is entirely optional and will be useful only after many runs have been completed.
        Your program never needs to make this call.
        """

        params = f'type=score&teamID={teamId}'

        response = self.__send_get_request(params, url_ending='score.php')
        return self.__validate(response)

    def get_my_team_last_x_runs(self, teamId, count=1):
        """
        Return Values: Your previous $count runs with score.
        """
        params = f'type=runs&teamID={teamId}&count=count'

        response = self.__send_get_request(params, url_ending='score.php')
        return self.__validate(response)

    def __validate(self, response):
        try:
            if not response:
                raise HTTPRequestFailureException

            data = response.json()
            if not data['code'] == 'OK':
                raise APIFailureException
            
            return data

        except HTTPRequestFailureException:
            print(f'Request has failed with {response.status_code} status code.')
            return None
        except APIFailureException:
            print(f'Api returned {data["code"]} code with the below message\n{data["message"]}' if data["message"] else ".")
            return None