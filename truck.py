



#creating a truck class
class Truck:
    def __init__(self, address, mileage, capacity, speed, package_id, load, delivery_time):
        self.address = address
        self.mileage = mileage
        self.capacity = capacity
        self.speed = speed
        self.package_id = package_id
        self.load = load or []
        self.delivery_time = delivery_time
        self.time = delivery_time

    def __str__(self):
        return f"address: {self.address}, mileage: {self.mileage}, capacity: {self.capacity}, speed: {self.speed}, " \
               f" package_id: {self.package_id}, load: {self.load}, delivery_time: {self.delivery_time}"

