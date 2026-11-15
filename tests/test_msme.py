import unittest
from msme.engine import MSME43BComplianceEngine, MSMEVendorInvoice

class TestMSMECompliance(unittest.TestCase):
    def test_msme_15_day_breach_without_agreement(self):
        engine = MSME43BComplianceEngine()
        # Micro enterprise invoice with no written agreement -> 15 days statutory limit
        inv = MSMEVendorInvoice(
            invoice_number="INV-MICRO-001",
            vendor_id="VEND-101",
            vendor_name="Precision Die Tools",
            udyam_registration_number="UDYAM-MH-12-0019284",
            enterprise_category="MICRO",
            invoice_date="2026-03-01",
            invoice_amount=500000.0,
            has_written_agreement=False,
            is_paid=False
        )

        # Assessment on March 25 (24 days after invoice date > 15 days)
        res = engine.evaluate_invoice(inv, assessment_date_str="2026-03-25")
        self.assertEqual(res.statutory_allowed_days, 15)
        self.assertEqual(res.statutory_due_date, "2026-03-16")
        self.assertEqual(res.days_overdue, 9)
        self.assertTrue(res.is_disallowed_for_tax_deduction)
        self.assertEqual(res.disallowed_expense_amount, 500000.0)
        # Tax exposure = 500,000 * 31.2% = 156,000
        self.assertEqual(res.corporate_tax_exposure_inr, 156000.0)
        self.assertEqual(res.status, "STATUTORY_BREACH_DISALLOWED")

    def test_medium_enterprise_exempt(self):
        engine = MSME43BComplianceEngine()
        inv = MSMEVendorInvoice(
            invoice_number="INV-MED-09",
            vendor_id="VEND-MED",
            vendor_name="National Steel Ltd",
            udyam_registration_number="UDYAM-GJ-01-0099881",
            enterprise_category="MEDIUM",
            invoice_date="2026-03-01",
            invoice_amount=1000000.0,
            has_written_agreement=True
        )
        res = engine.evaluate_invoice(inv, assessment_date_str="2026-05-15")
        self.assertFalse(res.is_applicable_under_43bh)
        self.assertFalse(res.is_disallowed_for_tax_deduction)

if __name__ == "__main__":
    unittest.main()
