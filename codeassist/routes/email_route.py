from fastapi import APIRouter
from codeassistant.source.emailBuddy import emailBuddy


email_router = APIRouter(
    prefix="/email",
    tags=["email"],
    responses={404: {"description": "Not found"}},
)


@email_router.post("/send-textual-email")
async def sendTextualEmail(email_template: dict):
    """ 
    {
        "receiver_email": "receiver_email",
        "content": "Email Content",
    }
    """
    receiver_email = email_template["receiver_email"]
    email_content = email_template["content"]
    e = emailBuddy()
    e.sendTextualEmail(receiver_email, email_content)

