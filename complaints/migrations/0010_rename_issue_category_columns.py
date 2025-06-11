from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0009_alter_issue_category_issuecategoryname'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL
            """
            ALTER TABLE complaints_issue_category 
            RENAME COLUMN "issueCategoryCode" TO "issue_category_code";
            ALTER TABLE complaints_issue_category 
            RENAME COLUMN "issueCategoryname" TO "issue_category_name";
            """,
            # Reverse SQL
            """
            ALTER TABLE complaints_issue_category 
            RENAME COLUMN "issue_category_code" TO "issueCategoryCode";
            ALTER TABLE complaints_issue_category 
            RENAME COLUMN "issue_category_name" TO "issueCategoryname";
            """
        ),
    ] 