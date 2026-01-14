from fastapi import APIRouter
from ..schemas.rewards import (
    UserRewards, ClaimReward
)
from ..reward_logic import (
    get_user_rewards, claim_reward
)

router = APIRouter(prefix="/v1/rewards", tags=["Rewards"])

@router.post("")
def attempt_get_user_rewards(user: UserRewards):
    return get_user_rewards(user.user_id)

@router.post("/claim")
def attempt_claim_reward(reward: ClaimReward):
    return claim_reward(reward.reward_id, reward.user_id)