"""MSME Section 43B(h) Statutory Payment Tracker, Tax Disallowance & Priority Disbursement Engine."""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class MSMEVendorInvoice:
    invoice_number: str
    vendor_id: str
    vendor_name: str
    udyam_registration_number: str
    enterprise_category: str  # MICRO, SMALL, MEDIUM
    invoice_date: str         # YYYY-MM-DD
    invoice_amount: float
    has_written_agreement: bool = False
    is_paid: bool = False
    payment_date: Optional[str] = None


@dataclass
class ComplianceAssessment:
    invoice_number: str
    vendor_name: str
    enterprise_category: str
    statutory_allowed_days: int  # 15 days if no agreement, max 45 days if written agreement
    statutory_due_date: str
    days_overdue: int
    is_applicable_under_43bh: bool
    is_disallowed_for_tax_deduction: bool
    disallowed_expense_amount: float
    corporate_tax_exposure_inr: float  # Tax @ 30% + 4% cess = 31.2%
    status: str  # COMPLIANT_PAID, WITHIN_DUE_DATE, STATUTORY_BREACH_DISALLOWED


class MSME43BComplianceEngine:
    """Income Tax Section 43B(h) statutory due-date tracker and expense disallowance calculator."""

    CORPORATE_TAX_RATE_WITH_CESS = 0.312  # 31.2%

    def evaluate_invoice(
        self,
        invoice: MSMEVendorInvoice,
        assessment_date_str: str
    ) -> ComplianceAssessment:
        # Medium enterprises are excluded from Section 43B(h)
        is_applicable = invoice.enterprise_category in ("MICRO", "SMALL")

        # Statutory limit: 45 days with agreement, 15 days without agreement
        statutory_days = 45 if invoice.has_written_agreement else 15

        inv_dt = datetime.strptime(invoice.invoice_date, "%Y-%m-%d").date()
        statutory_due_dt = inv_dt + timedelta(days=statutory_days)
        statutory_due_str = statutory_due_dt.strftime("%Y-%m-%d")

        asmt_dt = datetime.strptime(assessment_date_str, "%Y-%m-%d").date()

        if invoice.is_paid and invoice.payment_date:
            pay_dt = datetime.strptime(invoice.payment_date, "%Y-%m-%d").date()
            overdue_days = max(0, (pay_dt - statutory_due_dt).days)
            is_disallowed = is_applicable and (pay_dt > statutory_due_dt)
            status = "COMPLIANT_PAID" if not is_disallowed else "PAID_AFTER_DUE_DATE_DISALLOWED"
        else:
            overdue_days = max(0, (asmt_dt - statutory_due_dt).days)
            is_disallowed = is_applicable and (asmt_dt > statutory_due_dt)
            status = "STATUTORY_BREACH_DISALLOWED" if is_disallowed else "WITHIN_DUE_DATE"

        if is_disallowed:
            disallowed_amount = invoice.invoice_amount
            tax_exposure = round(disallowed_amount * self.CORPORATE_TAX_RATE_WITH_CESS, 2)
        else:
            disallowed_amount = 0.0
            tax_exposure = 0.0

        return ComplianceAssessment(
            invoice_number=invoice.invoice_number,
            vendor_name=invoice.vendor_name,
            enterprise_category=invoice.enterprise_category,
            statutory_allowed_days=statutory_days,
            statutory_due_date=statutory_due_str,
            days_overdue=overdue_days,
            is_applicable_under_43bh=is_applicable,
            is_disallowed_for_tax_deduction=is_disallowed,
            disallowed_expense_amount=disallowed_amount,
            corporate_tax_exposure_inr=tax_exposure,
            status=status
        )
