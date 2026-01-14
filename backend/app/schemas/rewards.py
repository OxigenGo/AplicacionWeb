from pydantic import BaseModel


class UserRewards(BaseModel):
    user_id: int
    
class ClaimReward(BaseModel):
    reward_id: int
    user_id: int