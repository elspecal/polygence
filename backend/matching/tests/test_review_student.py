from django.test import TestCase
from rest_framework.test import APIClient

from matching.models import Mentor, MentorRequest, StudentProposal
from matching.services.student_proposal import StudentProposalService


class ReviewStudentPostTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)

    def test_records_accept_response(self):
        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.ACCEPT},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.ACCEPT)

    def test_records_reject_response(self):
        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.REJECT},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.REJECT)

    def test_rejects_second_response(self):
        StudentProposalService.update_response(self.proposal, StudentProposal.ACCEPT)

        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.REJECT},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Response already recorded")


class ReviewStudentPatchNoDecision(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(
            mentor=self.mentor, mentor_request=self.mentor_request
        )

    def test_rejects_decline_reason(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"unavailable_until": True}},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No decision to follow-up yet")
        self.proposal.refresh_from_db()
        self.assertNotIn("reason", self.proposal.response)

    def test_rejects_match_rating(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"match_rating": 9},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No decision to follow-up yet")
        self.proposal.refresh_from_db()
        self.assertNotIn("match_rating", self.proposal.response)


class ReviewStudentPatchAccapted(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(
            mentor=self.mentor, mentor_request=self.mentor_request
        )
        StudentProposalService.update_response(self.proposal, StudentProposal.ACCEPT)

    def test_records_match_rating(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"match_rating": 5},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["match_rating"], 5)

    def test_rejects_decline_reason(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_good_fit": True}},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Mismatched follow-up")
        self.proposal.refresh_from_db()
        self.assertNotIn("reason", self.proposal.response)

    def test_rejects_decline_reason_and_match_rating(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"timezone_issue": True}, "match_rating": 4},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Mismatched follow-up")
        self.proposal.refresh_from_db()
        self.assertNotIn("reason", self.proposal.response)
        self.assertNotIn("match_rating", self.proposal.response)


class ReviewStudentPatchRejectedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(
            mentor=self.mentor, mentor_request=self.mentor_request
        )
        StudentProposalService.update_response(self.proposal, StudentProposal.REJECT)

    def test_records_decline_reason(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_good_fit": True}},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["reason"], {"no_good_fit": True})

    def test_rejects_match_rating(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"match_rating": 8},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Mismatched follow-up")
        self.proposal.refresh_from_db()
        self.assertNotIn("match_rating", self.proposal.response)

    def test_rejects_match_rating_and_decline_reason(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_good_fit": True}, "match_rating": 7},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Mismatched follow-up")
        self.proposal.refresh_from_db()
        self.assertNotIn("reason", self.proposal.response)
        self.assertNotIn("match_rating", self.proposal.response)

    def test_rejects_second_reason(self):
        self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_bandwidth": True}},
            format="json",
        )

        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"timezone_issue": True}},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Reason already recorded")


class ProposalActiveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)

    def test_returns_student_and_open_status(self):
        response = self.client.get(f"/api/proposal-active/{self.proposal.uuid}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["student_name"], "Jamie")
        self.assertFalse(response.data["is_matched"])
        self.assertIsNone(response.data["response_value"])
