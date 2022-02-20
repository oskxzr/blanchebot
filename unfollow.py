from instagrapi import Client
InstagramClient = Client()
InstagramClient.login("blancheofsaintandre", "REDACTED")
ClientId = InstagramClient.user_id_from_username("blancheofsaintandre")
Following = InstagramClient.user_following(ClientId)
for UserId in Following:
    try:
       print("Unfollowing: " + UserId)
       InstagramClient.user_unfollow(UserId) 
    except Exception as e:
        print(e)
