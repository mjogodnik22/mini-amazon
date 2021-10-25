from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT o.oid, uid, pid, time_purchased
FROM OrderInformation o, ItemsInOrder i
WHERE oid = :id
AND o.oid = i.oid
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT o.oid, uid, pid, time_purchased
FROM OrderInformation o, ItemsInOrder i
WHERE uid = :uid
AND o.oid = i.oid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
