import stripe
from decouple import config
DJANGO_DEBUG=config('DJANGO_DEBUG', default=False, cast=bool)
STRIPE_SECRET_KEY=config('STRIPE_SECRET_KEY', default="", cast=str)

if 'sk_test' in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
  raise ValueError("Invalid stripe key for prod")

stripe.api_key = STRIPE_SECRET_KEY
def create_customer(name="",
                    email="",
                    metadata={},
                    raw=False):
  response = stripe.Customer.create(
      name=name,
      email=email,
      metadata=metadata
)
  if raw:
    return response
  stripe_id = response.id
  return response.id

def create_product(name="",
                    metadata={},
                    raw=False):
  response = stripe.Customer.create(
      name=name,
      metadata=metadata
)
  if raw:
    return response
  stripe_id = response.id
  return response.id



  def create_price(
        currency="inr",
        unit_amount="9999",
        interval="month",
        product_data=None,
        metadata={}, 
        raw=False):
    if response is None:
      return None
    response = stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        recurring={"interval":interval},
        product_data=product,
        metadata=metadata
      )
  if raw:
    return response
  stripe_id = response.id
  return response.id







