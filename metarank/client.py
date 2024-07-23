from requests import request

from .schemas import (FeedbackSchema, FeedbackResponse, TrainResponse,
                      RankResponse, RecommendResponse, RecommendSchema,
                      InferenceEncoderSchema, InferenceEncoderResponse,
                      InferenceCrossSchema, InferenceCrossResponse, RankSchema)


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def feedback(self, feedback_data: FeedbackSchema) -> FeedbackResponse:
        """
        See: https://docs.metarank.ai/reference/api#feedback
        
        :param feedback_data: 
        :return: 
        """
        response = self.request("POST", "feedback", feedback_data.dict(exclude_none=True))
        return FeedbackResponse(**response)
    
    def health_check(self) -> bool:
        """
        :return: Whether the metarank service is ready or not 
        """

        response = self.raw_request('GET', 'health')
        return response.ok
    
    def inference_encoder(self, name: str, inference_encoder_data: InferenceEncoderSchema):
        """
        See: https://docs.metarank.ai/reference/api#inference-with-llms

        :param name: 
        :param inference_encoder_data: 
        :return: 
        """

        response = self.request("POST", f"inference/encoder/{name}", inference_encoder_data.dict(exclude_none=True))
        return InferenceEncoderResponse(**response)
    
    def inference_cross(self, name: str, inference_cross_data: InferenceCrossSchema):
        """
        See: https://docs.metarank.ai/reference/api#inference-with-llms

        :param name: 
        :param inference_cross_data: 
        :return: 
        """

        response = self.request("POST", f"inference/cross/{name}", inference_cross_data.dict(exclude_none=True))
        return InferenceCrossResponse(**response)
    
    def metrics(self) -> str:
        """
        See: https://docs.metarank.ai/reference/api#prometheus-metrics

        :return: 
        """
        
        response = self.raw_request("GET", "metrics")
        return response.text
    
    def rank(self, model_name: str, rank_data: RankSchema, explain: bool = False):
        """
        See: https://docs.metarank.ai/reference/api#ranking

        :param model_name: 
        :param explain: 
        :return: 
        """

        endpoint = f"rank/{model_name}"
        if explain:
            endpoint = f"{endpoint}?explain=1"

        response = self.request("POST", endpoint, data=rank_data.dict(exclude_none=True))
        return RankResponse(**response)
    
    def recommend(self, model_name: str, data: RecommendSchema) -> RecommendResponse:
        """
        See: https://docs.metarank.ai/reference/api#recommendations

        :param model_name: 
        :param data: 
        :return: 
        """

        endpoint = f"recommend/{model_name}"
        
        response = self.request("POST", endpoint, data=data)
        return RecommendResponse(**response)
    
    def train(self, model_name: str):
        """
        See: https://docs.metarank.ai/reference/api#train

        :param model_name: 
        :return: 
        """

        response = self.request("POST", f"train/{model_name}")
        return TrainResponse(**response)

    def request(self, method, endpoint, data=None):
        headers = {'Content-Type': 'application/json'}
        response = self.raw_request(method, endpoint, json=data, headers=headers)
        self._handle_error(response)
        return response.json()

    def raw_request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return request(method, url, **kwargs)

    @staticmethod
    def _handle_error(response):
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
