app_name = "proserv_erp"
app_title = "ProEdge"
app_publisher = "Your Company"
app_description = "Full-suite ERP for Professional Services firms"
app_email = "dev@yourcompany.com"
app_license = "MIT"
app_version = "0.0.1"

required_apps = ["frappe", "bizaxl_erp"]

app_include_css = "/assets/proserv_erp/css/proserv_erp.css"
app_include_js = "/assets/proserv_erp/js/proserv_erp.js"

doc_events = {}

scheduler_events = {
    "daily": [],
    "weekly": [],
}


override_doctype_class = {
    "Service Category": "proserv_erp.professional_services.doctype.service_category.service_category.ServiceCategory",
    "Service": "proserv_erp.professional_services.doctype.service.service.Service",
    "Rate Card": "proserv_erp.professional_services.doctype.rate_card.rate_card.RateCard",
    "Rate Card Item": "proserv_erp.professional_services.doctype.rate_card_item.rate_card_item.RateCardItem",
    "Staff Profile": "proserv_erp.professional_services.doctype.staff_profile.staff_profile.StaffProfile",
    "Staff Skill": "proserv_erp.professional_services.doctype.staff_skill.staff_skill.StaffSkill",
    "Staff Certification": "proserv_erp.professional_services.doctype.staff_certification.staff_certification.StaffCertification",
    "Expense Category": "proserv_erp.professional_services.doctype.expense_category.expense_category.ExpenseCategory",
    "Client": "proserv_erp.professional_services.doctype.client.client.Client",
    "Client Contact": "proserv_erp.professional_services.doctype.client_contact.client_contact.ClientContact",
    "PS Lead": "proserv_erp.professional_services.doctype.lead.lead.PSLead",
    "Opportunity": "proserv_erp.professional_services.doctype.opportunity.opportunity.Opportunity",
    "Practice Certificate": "proserv_erp.professional_services.doctype.practice_certificate.practice_certificate.PracticeCertificate",
    "Professional Indemnity Policy": "proserv_erp.professional_services.doctype.professional_indemnity_policy.professional_indemnity_policy.ProfessionalIndemnityPolicy",
    "Engagement Team Member": "proserv_erp.professional_services.doctype.engagement_team_member.engagement_team_member.EngagementTeamMember",
    "Engagement Deliverable": "proserv_erp.professional_services.doctype.engagement_deliverable.engagement_deliverable.EngagementDeliverable",
    "Engagement": "proserv_erp.professional_services.doctype.engagement.engagement.Engagement",
    "Engagement Milestone": "proserv_erp.professional_services.doctype.engagement_milestone.engagement_milestone.EngagementMilestone",
    "Conflict Check Party": "proserv_erp.professional_services.doctype.conflict_check_party.conflict_check_party.ConflictCheckParty",
    "Conflict Check": "proserv_erp.professional_services.doctype.conflict_check.conflict_check.ConflictCheck",
    "Resource Allocation": "proserv_erp.professional_services.doctype.resource_allocation.resource_allocation.ResourceAllocation",
    "Timesheet Entry": "proserv_erp.professional_services.doctype.timesheet_entry.timesheet_entry.TimesheetEntry",
    "Expense Claim Item": "proserv_erp.professional_services.doctype.expense_claim_item.expense_claim_item.ExpenseClaimItem",
    "Expense Claim": "proserv_erp.professional_services.doctype.expense_claim.expense_claim.ExpenseClaim",
    "Retainer Agreement": "proserv_erp.professional_services.doctype.retainer_agreement.retainer_agreement.RetainerAgreement",
    "Proforma Invoice Item": "proserv_erp.professional_services.doctype.proforma_invoice_item.proforma_invoice_item.ProformaInvoiceItem",
    "Proforma Invoice": "proserv_erp.professional_services.doctype.proforma_invoice.proforma_invoice.ProformaInvoice",
    "Fee Note Milestone": "proserv_erp.professional_services.doctype.fee_note_milestone.fee_note_milestone.FeeNoteMilestone",
    "Fee Note Timesheet": "proserv_erp.professional_services.doctype.fee_note_timesheet.fee_note_timesheet.FeeNoteTimesheet",
    "Fee Note Expense": "proserv_erp.professional_services.doctype.fee_note_expense.fee_note_expense.FeeNoteExpense",
    "Fee Note": "proserv_erp.professional_services.doctype.fee_note.fee_note.FeeNote",
    "Retainer Consumption": "proserv_erp.professional_services.doctype.retainer_consumption.retainer_consumption.RetainerConsumption",
    "Write Off": "proserv_erp.professional_services.doctype.write_off.write_off.WriteOff",
    "Engagement Document": "proserv_erp.professional_services.doctype.engagement_document.engagement_document.EngagementDocument",
    "Document Template": "proserv_erp.professional_services.doctype.document_template.document_template.DocumentTemplate",
    "Proposal Service Item": "proserv_erp.professional_services.doctype.proposal_service_item.proposal_service_item.ProposalServiceItem",
    "Proposal": "proserv_erp.professional_services.doctype.proposal.proposal.Proposal",
    "Letter of Engagement": "proserv_erp.professional_services.doctype.letter_of_engagement.letter_of_engagement.LetterOfEngagement",
    "Business Development Activity": "proserv_erp.professional_services.doctype.business_development_activity.business_development_activity.BusinessDevelopmentActivity",
    "Referral": "proserv_erp.professional_services.doctype.referral.referral.Referral",
    "Client Satisfaction Survey": "proserv_erp.professional_services.doctype.client_satisfaction_survey.client_satisfaction_survey.ClientSatisfactionSurvey",
    "Internal Review": "proserv_erp.professional_services.doctype.internal_review.internal_review.InternalReview",
    "Complaint": "proserv_erp.professional_services.doctype.complaint.complaint.Complaint",
    "Compliance Obligation": "proserv_erp.professional_services.doctype.compliance_obligation.compliance_obligation.ComplianceObligation",
    "KYC Record": "proserv_erp.professional_services.doctype.kyc_record.kyc_record.KYCRecord",
    "Regulatory Filing": "proserv_erp.professional_services.doctype.regulatory_filing.regulatory_filing.RegulatoryFiling",
    "Retainer Task Log": "proserv_erp.professional_services.doctype.retainer_task_log.retainer_task_log.RetainerTaskLog",
    "Retainer Review": "proserv_erp.professional_services.doctype.retainer_review.retainer_review.RetainerReview",
    "Capacity Plan Staff": "proserv_erp.professional_services.doctype.capacity_plan_staff.capacity_plan_staff.CapacityPlanStaff",
    "Capacity Plan": "proserv_erp.professional_services.doctype.capacity_plan.capacity_plan.CapacityPlan",
    "Engagement Profitability": "proserv_erp.professional_services.doctype.engagement_profitability.engagement_profitability.EngagementProfitability",
    "Practice Area Dashboard": "proserv_erp.professional_services.doctype.practice_area_dashboard.practice_area_dashboard.PracticeAreaDashboard",
    "Client Profitability": "proserv_erp.professional_services.doctype.client_profitability.client_profitability.ClientProfitability",
}

after_install = "proserv_erp.install.after_install"

fixtures = [
    {"doctype": "Workspace", "filters": [["name", "in", ["ProEdge"]]]},
    {"doctype": "Notification", "filters": [["document_type", "in", [
        "Fee Note", "Engagement", "Engagement Milestone", "Retainer Agreement",
        "Retainer Consumption", "KYC Record", "Practice Certificate",
        "Professional Indemnity Policy", "Compliance Obligation",
        "Regulatory Filing", "Resource Allocation", "Proposal", "PS Lead",
        "Timesheet Entry", "Client Satisfaction Survey"
    ]]]},
]
