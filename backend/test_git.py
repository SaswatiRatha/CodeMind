from app.services.repository_service import clone_repository

result = clone_repository("https://github.com/octocat/Hello-World.git", "data/service-test")

print(result)