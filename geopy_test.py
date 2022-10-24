from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Penguin Academy")

#Penguin House 2.0
# Latitude = "-25.30217479154702"
# Longitude = "-57.5810750729888"

# Mi casa en encarnacion
# Latitude = "-27.340194049662397"
# Longitude = "-55.85253220006652"

# Penguin Palace Villarica
# Latitude = "-25.782089831170122"
# Longitude = "-56.451750374209844"

# Ubicacion libre de test
Latitude = "-25.30993055741617"
Longitude = "-57.63060171020841"

location = geolocator.reverse(Latitude + "," + Longitude)

# print(location)
print(type(location))

address = location.raw['address']

print(address)
print(type(address))


for cosito in location:
    print("--------------------")
    print(cosito)

city = address.get('city', '')
state = address.get('state', '')
region = address.get('region','')
country = address.get('country', '')
code = address.get('country_code')
zipcode = address.get('postcode')


print('City : ',city)
print('State : ',state)
print('Region : ',region)
print('Country : ',country)
print('Zip Code : ', zipcode)