from db.model import Submission

def submission(submission: Submission) -> str:
    return (
        f"<b>Sender:</b> {submission.submitter_name}\n"
        f"<b>Original:</b>\n{submission.message}\n\n"
        f"<b>Gossip Girl Voice:</b>\n{submission.gg_voice_final}"
    )