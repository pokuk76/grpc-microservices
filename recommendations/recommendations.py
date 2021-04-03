"""
Implementing the RPC server
"""
# Python Libraries
from concurrent import futures
import random
# Installed Packages
import grpc
# App Packages
from recommendations_pb2 import BookCategory, BookRecommendation, RecommendationResponse
import recommendations_pb2_grpc

#  In a real application this would be in a database somewhere
books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=4, title="The Hitchhiker's Guide to the Galaxy"),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),

    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=7, title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id=8, title="How to Win Friends and Influence People"),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    """
    Implementation of the Book Recommendation microservice
    Inherits from RecommendationsServicer
    """

    def Recommend(self, request, context):
        """
        Returns a list of book recommendations

        Implementation of Recommend service in protobuf specification, and must match API specification in protobuf

            Parameters:
                request (RecommendationRequest):
                context ():
        """
        
        if request.category not in books_by_category:
            # TODO: make the error handling nicer (we'll be using interceptors?)
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]  # An array holding the books for that category
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()