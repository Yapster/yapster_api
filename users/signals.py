from django.dispatch import Signal

account_created = Signal(providing_args=["info","user"])
account_modified = Signal(providing_args=["info","user_id"])
user_verified = Signal(providing_args=["user"])
user_unverified = Signal(providing_args = ["user"])
user_recommended = Signal(providing_args=["user"])
user_unrecommended = Signal(providing_args=["user"])
profile_picture_edited = Signal(providing_args=["info","user","profile_picture_flag","profile_picture_path","profile_picture_cropped_flag","profile_picture_cropped_path"])
profile_picture_deleted = Signal(providing_args=["info","user"])
user_edited = Signal(providing_args=["info","user"])
profile_edited = Signal(providing_args=["info","user"])
settings_edited = Signal(providing_args=["info","user"])
posts_are_private_turned_on = Signal(providing_args=["user"])
posts_are_private_turned_off = Signal(providing_args=["user"])
first_yap_notification_to_all_followers = Signal(providing_args=["user","yap"])

#Delete User Signals
account_deleted_or_deactivated = Signal(providing_args=["user_info"])
#Activate User Signals
user_activated_and_is_user_activated = Signal(providing_args=["user"])
account_reactivated = Signal(providing_args=["user"])

#Facebook Signals
new_facebook_friend_joined_yapster = Signal(providing_args=["user","facebook_access_token"])
facebook_friend_newly_connected_to_facebook = Signal(providing_args=["user","facebook_access_token"])

#Twitter Signals
account_created_twitter = Signal(providing_args=["user"])
