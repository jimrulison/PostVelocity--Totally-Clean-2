# This is a fixed version of the payment section to replace emergentintegrations with direct Stripe usage

import stripe

# Initialize Stripe
stripe_api_key = os.getenv("STRIPE_API_KEY")
if not stripe_api_key:
    print("Warning: STRIPE_API_KEY not found in environment")
    stripe_api_key = "sk_test_default"  # Fallback for development
stripe.api_key = stripe_api_key

@app.post("/api/payments/create-checkout")
async def create_payment_checkout(request: dict):
    """Create Stripe checkout session for plan or add-on purchase"""
    try:
        # Get the host URL from request
        host_url = request.get("host_url", "http://localhost:3000")
        
        plan_type = request.get("plan_type")
        plan_interval = request.get("plan_interval", "monthly")
        addon_type = request.get("addon_type")
        addon_tier = request.get("addon_tier")
        user_id = request.get("user_id", "demo-user")
        
        # Calculate amount based on plan or add-on
        amount = 0.0
        item_name = ""
        
        if plan_type:
            # Plan purchase
            amount = get_plan_price(plan_type, plan_interval)
            plan_config = PLAN_CONFIGS.get(plan_type, {})
            item_name = f"{plan_config.get('name', plan_type.title())} - {plan_interval.title()}"
        elif addon_type and addon_tier:
            # Add-on purchase
            addon_config = ADDON_CONFIGS.get(addon_type, {})
            tier_config = addon_config.get("tiers", {}).get(addon_tier, {})
            amount = tier_config.get("price", 0.0)
            item_name = f"{addon_config.get('name', addon_type.title())} - {addon_tier.title()}"
        else:
            raise HTTPException(status_code=400, detail="Either plan_type or addon_type/addon_tier required")
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid plan or add-on configuration")
        
        # Create checkout session request URLs
        success_url = f"{host_url}/dashboard?session_id={{CHECKOUT_SESSION_ID}}&payment_success=true"
        cancel_url = f"{host_url}/dashboard?payment_canceled=true"
        
        metadata = {
            "user_id": user_id,
            "item_name": item_name,
            "payment_type": "subscription" if plan_type else "addon"
        }
        
        if plan_type:
            metadata["plan_type"] = plan_type
            metadata["plan_interval"] = plan_interval
        if addon_type:
            metadata["addon_type"] = addon_type
            metadata["addon_tier"] = addon_tier
        
        # Create Stripe checkout session using direct API
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item_name,
                    },
                    'unit_amount': int(amount * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        
        # Store transaction record
        transaction_data = {
            "user_id": user_id,
            "session_id": session.id,
            "amount": amount,
            "currency": "usd",
            "payment_status": "initiated",
            "plan_type": plan_type,
            "plan_interval": plan_interval,
            "addon_type": addon_type,
            "metadata": metadata,
            "created_at": datetime.utcnow()
        }
        
        result = await db.payment_transactions.insert_one(transaction_data)
        transaction_data["id"] = str(result.inserted_id)
        del transaction_data["_id"]
        
        return {
            "status": "success",
            "checkout_url": session.url,
            "session_id": session.id,
            "transaction": transaction_data
        }
    
    except Exception as e:
        print(f"Create checkout error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create checkout: {str(e)}")

@app.get("/api/payments/status/{session_id}")
async def get_payment_status(session_id: str):
    """Get payment status from Stripe and update database"""
    try:
        # Get status from Stripe using direct API
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Find transaction in database
        transaction = await db.payment_transactions.find_one({"session_id": session_id})
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Update transaction status if payment is complete and not already processed
        if session.payment_status == "paid" and transaction.get("payment_status") != "paid":
            # Update transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": "paid",
                        "completed_at": datetime.utcnow(),
                        "stripe_payment_intent_id": session.payment_intent
                    }
                }
            )
            
            # Process the subscription/addon purchase
            await process_successful_payment(transaction, session)
        
        return {
            "status": "success",
            "payment_status": session.payment_status,
            "session_status": session.status,
            "amount": session.amount_total / 100 if session.amount_total else 0,  # Convert from cents
            "currency": session.currency
        }
    
    except Exception as e:
        print(f"Get payment status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get payment status: {str(e)}")