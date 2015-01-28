from django.dispatch import Signal

user_tag_notification = Signal(providing_args=['yap'])
first_five_following_followed_get_yaps = Signal(providing_args=['user','user_requested'])
first_five_following_followed_make_stream_objects = Signal(providing_args=['user','first_five_following_yaps'])

yap_created = Signal(providing_args=["yap"])
yap_deleted = Signal(providing_args=["yap"])
yap_activated = Signal(providing_args=["yap"])

like_created = Signal(providing_args=["like"])
like_deleted = Signal(providing_args=["like"])
like_activated = Signal(providing_args=["like"])

reyap_created = Signal(providing_args=["reyap"])
reyap_deleted = Signal(providing_args=["reyap"])
reyap_activated = Signal(providing_args=["reyap"])

listen_created = Signal(providing_args=["listen"])

#send to requested user when a user requests them if they are private
follower_requested = Signal(providing_args=["follower_request"])
#send to requesting user when a private user accepts them
follower_accepted = Signal(providing_args=["follower_request"])
#send to requested user when someone requests them (due to auto accept when not private)
follower_new = Signal(providing_args=["follower_request"])
follower_deleted = Signal(providing_args=["follower_request"])
follower_activated = Signal(providing_args=["follower_request"])

#called if it is one of the users first x (10) listens
first_followings = Signal(providing_args=["follower_request"])

#Delete Listen Signals
listen_deleted = Signal(providing_args=["listen"])
#Activate Listen Signals 
listen_activated = Signal(providing_args=["listen"])

#Delete Listen Click Signals
listen_click_deleted = Signal(providing_args=["listen_click"])
#Activate Listen Click Signals
listen_click_activated = Signal(providing_args=["listen_click"])

#Delete Yap Signals
yap_deleted = Signal(providing_args=["yap"])
#Activate Yap Signals
yap_activated = Signal(providing_args=["yap"])

#Delete Reyap Signals
reyap_deleted = Signal(providing_args=["reyap"])
#Activate Reyap Signals
reyap_activated = Signal(providing_args=["reyap"])

#Delete Like Signals
like_deleted = Signal(providing_args=["like"])
#Activate Reyap Signals
like_activated = Signal(providing_args=["like"])

#Unfollow Follower Request Signals
follower_request_unfollowed = Signal(providing_args=["follower_request"])

#Unrequested Follower Request Signal
follower_request_unrequested = Signal(providing_args=["follower_request"])

#Delete Follower Request Signals
follower_request_deleted = Signal(providing_args=["follower_request"])
#Activate Follower Request Signals
follower_request_activated = Signal(providing_args=["follower_request"])





