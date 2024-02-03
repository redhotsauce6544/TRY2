



class Packages:
    def __init__(self, package_ID, address, city, state, zipcode, deadline, weight, status="currently at hub"):
        self.package_ID = package_ID
        self.address = address
        self.state = state
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.deadline = deadline
        self.depature_time = None
        self.delivery_time = None




    def __str__(self):
        return f"ID: {self.package_ID}, address: {self.address}, city: {self.city}, state: {self.state}, " \
               f"zipcode: {self.zipcode}, deadline: {self.deadline}, weight: {self.weight}, status: {self.status}"



