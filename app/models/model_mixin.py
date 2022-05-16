from app.database import db_session


class ModelMixin:
    def save(self, commit=True):
        """Save this model to the database."""
        db_session.add(self)
        if commit:
            db_session.commit()
        else:
            # this will give opportunity to rollback the operation
            db_session.flush()
            db_session.refresh(self)
        return self

    def delete(self, commit=True):
        """Delete instance"""
        db_session.delete(self)
        if commit:
            db_session.commit()
        return self

    def rollback(self):
        """Rollback transaction"""
        db_session.rollback()
        return self

    def commit(self):
        """Commit transaction"""
        db_session.commit()
        return self
