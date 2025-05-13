# stuff inside router.py
############################################################################
@router.get("/v1/member/get", response_model=AlyfMember)
async def get_member_data(
    id: str = Query(None, description="Member ID"),
    email: Optional[str] = Query(None, description="Member email"),
    phone_number: Optional[str] = Query(None, description="Member phone number")
):
    """
    Get member data by ID, email, or phone number.
    
    At least one parameter must be provided.
    """
    return get_member_by_criteria(
        member_id=id,
        email=email,
        phone_number=phone_number
    )
# stuff inside apc_apis.py
#############################################################################
def get_member_by_criteria(member_id=None, email=None, phone_number=None):
    """
    Get member data by ID, email, or phone number.
    
    Args:
        member_id: Member ID
        email: Member email
        phone_number: Member phone number
        
    Returns:
        AlyfMember object with member data
    """
   
    if not any([member_id, email, phone_number]):
        raise HTTPException(status_code=400, detail="At least one of id, email, or phone_number required")
    
    kwargs = {"identifier": member_id} if member_id else {"email": email} if email else {"phone_number": phone_number}
    member_data = ALYF_MEMBER_OPS.get(**kwargs)
    
    if not member_data:
        raise HTTPException(
            status_code=404, 
            detail=f"Member not found for the provided criteria. id: {member_id or 'null'}, "
                   f"email: {email or 'null'}, phone number: {phone_number or 'null'}"
        )
    
    provider = ALYF_PROVIDER_OPS.get(member_data.get("provider_id", ""))
    provider_full_name = f"{provider.get('first_name', '')} {provider.get('last_name', '')}" if provider else None

    return AlyfMember(
        member_id=member_data.get("member_id", ""), 
        provider_id=member_data.get("provider_id", ""),
        first_name=member_data.get("first_name", ""), 
        last_name=member_data.get("last_name", ""),
        email=member_data.get("email", ""), 
        synth=member_data.get("synth", False),
        create_time=member_data.get("create_time", datetime.datetime.now()),
        update_time=member_data.get("update_time", datetime.datetime.now()),
        gender=member_data.get("gender"), 
        address=member_data.get("address"),
        date_of_birth=member_data.get("date_of_birth"),
        fallback_time_zone=member_data.get("fallback_time_zone", "UTC"),
        height=member_data.get("height"), 
        phone_number=member_data.get("phone_number"),
        provider_full_name=provider_full_name
    )