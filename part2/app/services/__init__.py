cat > part2/app/services/__init__.py << 'EOF'
#!/usr/bin/python3
"""Service layer package."""

from app.services.facade import HBnBFacade

facade = HBnBFacade()
EOF
