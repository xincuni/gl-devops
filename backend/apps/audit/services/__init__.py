from apps.audit.models import AuditLog


def write_audit_log(*, module, action, operator=None, target_type="", target_id="", detail=None):
    return AuditLog.objects.create(
        module=module,
        action=action,
        operator=operator,
        target_type=target_type,
        target_id=target_id,
        detail=detail or {},
    )
