from app.services.utils.user_utility import UserUtility


class UserDataController():

    @staticmethod
    def view_users_data():

        # Fetch only users with role of 'customer'
        users = UserUtility.get_all_customers()

        formatted_data = []
        for user in users:
            fu = UserUtility.format_user_data_for_view(user)
            formatted_data.append(fu)

        return formatted_data

