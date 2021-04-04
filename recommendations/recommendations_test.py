from recommendations import RecommendationService

from recommendations_pb2 import BookCategory, RecommendationRequest

def test_recommendations():
    service = RecommendationService()
    request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=1
    )
    response = service.Recommend(request, None) # Setting context to None -> what does that mean?
    ''' Passing None for the context "works as long as you don't use it"
        We're use context.abort when the BookCategory requested doesn't exist so as long as we don't do that
    '''
    assert len(response.recommendations) == 1