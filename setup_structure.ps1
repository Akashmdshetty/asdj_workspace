
# Define the project root
$projectRoot = "C:\Users\aakas\OneDrive\Desktop\saas-collab"

# Define directories to create
$directories = @(
    "backend",
    "backend\config",
    "backend\config\settings",
    "backend\core",
    "backend\core\models",
    "backend\core\permissions",
    "backend\core\middleware",
    "backend\core\managers",
    "backend\core\services",
    "backend\core\utils",
    "backend\documents",
    "backend\documents\models",
    "backend\documents\api",
    "backend\documents\services",
    "backend\documents\selectors",
    "backend\collaboration",
    "backend\collaboration\consumers",
    "backend\collaboration\presence",
    "backend\collaboration\pubsub",
    "backend\audit",
    "backend\billing",
    "backend\workers",
    "backend\tests",
    "backend\tests\factories",
    "backend\tests\unit",
    "backend\tests\integration",
    "backend\tests\e2e",
    "backend\requirements",
    "frontend",
    "frontend\src",
    "frontend\public",
    "docker"
)

# Define files to create
$files = @(
    "backend\manage.py",
    "backend\config\__init__.py",
    "backend\config\asgi.py",
    "backend\config\wsgi.py",
    "backend\config\celery.py",
    "backend\config\routing.py",
    "backend\config\urls.py",
    "backend\config\logging.py",
    "backend\config\settings\__init__.py",
    "backend\config\settings\base.py",
    "backend\config\settings\local.py",
    "backend\config\settings\production.py",
    "backend\core\__init__.py",
    "backend\core\models\__init__.py",
    "backend\core\models\tenant.py",
    "backend\core\models\user.py",
    "backend\core\models\membership.py",
    "backend\core\permissions\__init__.py",
    "backend\core\permissions\roles.py",
    "backend\core\permissions\permissions.py",
    "backend\core\permissions\engine.py",
    "backend\core\middleware\__init__.py",
    "backend\core\middleware\tenant.py",
    "backend\core\middleware\auth.py",
    "backend\core\managers\__init__.py",
    "backend\core\managers\tenant_queryset.py",
    "backend\core\services\__init__.py",
    "backend\core\services\tenant_service.py",
    "backend\core\services\user_service.py",
    "backend\core\utils\__init__.py",
    "backend\core\utils\ids.py",
    "backend\core\utils\time.py",
    "backend\documents\__init__.py",
    "backend\documents\models\__init__.py",
    "backend\documents\models\document.py",
    "backend\documents\models\snapshot.py",
    "backend\documents\models\operation.py",
    "backend\documents\api\__init__.py",
    "backend\documents\api\serializers.py",
    "backend\documents\api\views.py",
    "backend\documents\api\urls.py",
    "backend\documents\services\__init__.py",
    "backend\documents\services\document_service.py",
    "backend\documents\services\merge_engine.py",
    "backend\documents\selectors\__init__.py",
    "backend\documents\selectors\document_selector.py",
    "backend\collaboration\__init__.py",
    "backend\collaboration\consumers\__init__.py",
    "backend\collaboration\consumers\base.py",
    "backend\collaboration\consumers\document.py",
    "backend\collaboration\consumers\presence.py",
    "backend\collaboration\routing.py",
    "backend\collaboration\presence\__init__.py",
    "backend\collaboration\presence\tracker.py",
    "backend\collaboration\presence\cleanup.py",
    "backend\collaboration\pubsub\__init__.py",
    "backend\collaboration\pubsub\broadcaster.py",
    "backend\collaboration\throttling.py",
    "backend\audit\__init__.py",
    "backend\audit\models.py",
    "backend\audit\services.py",
    "backend\audit\tasks.py",
    "backend\billing\__init__.py",
    "backend\billing\models.py",
    "backend\billing\services.py",
    "backend\billing\webhooks.py",
    "backend\billing\tasks.py",
    "backend\workers\__init__.py",
    "backend\workers\document_tasks.py",
    "backend\workers\presence_tasks.py",
    "backend\workers\cleanup_tasks.py",
    "backend\tests\__init__.py",
    "backend\requirements\base.txt",
    "backend\requirements\local.txt",
    "backend\requirements\production.txt",
    "frontend\package.json",
    "docker\web.Dockerfile",
    "docker\worker.Dockerfile",
    "docker\redis.conf",
    "render.yaml",
    ".env.example",
    ".gitignore",
    "README.md"
)

# Create directories
foreach ($dir in $directories) {
    $path = Join-Path $projectRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
        Write-Host "Created directory: $path"
    }
}

# Create files
foreach ($file in $files) {
    $path = Join-Path $projectRoot $file
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Force -Path $path | Out-Null
        Write-Host "Created file: $path"
    }
}

Write-Host "Project structure creation complete."
