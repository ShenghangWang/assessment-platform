# Generated manually for the starter repo.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='AssessmentPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=300)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.IntegerField()),
                ('status', models.CharField(default='published', max_length=20)),
                ('config_json', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='core.assessmentpack')),
            ],
            options={
                'unique_together': {('pack', 'version_number')},
            },
        ),
        migrations.CreateModel(
            name='AssessmentAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_token', models.CharField(blank=True, max_length=128, null=True)),
                ('status', models.CharField(default='in_progress', max_length=20)),
                ('final_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('display_score', models.IntegerField(blank=True, null=True)),
                ('band_key', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('meta_json', models.JSONField(blank=True, default=dict)),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assessmentpack')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assessmentversion')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_key', models.CharField(max_length=100)),
                ('raw_value', models.CharField(max_length=100)),
                ('normalized_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.assessmentattempt')),
            ],
            options={
                'unique_together': {('attempt', 'question_key')},
            },
        ),
        migrations.CreateModel(
            name='GeneratedReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_key', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField()),
                ('content_json', models.JSONField()),
                ('model_name', models.CharField(blank=True, max_length=100)),
                ('prompt_version', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attempt', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='core.assessmentattempt')),
            ],
        ),
    ]
