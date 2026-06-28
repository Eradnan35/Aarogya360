import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.user import Role

logger = logging.getLogger(__name__)

DEFAULT_ROLES = [
    "Admin",
    "Doctor",
    "Receptionist",
    "Lab Technician",
    "System Administrator",
]

async def seed_roles(session: AsyncSession) -> None:
    """
    Idempotent function to seed default roles into the database.
    It checks for the existence of each role and only creates it if it's missing.
    """
    logger.info("Starting role seeding...")
    
    for role_name in DEFAULT_ROLES:
        stmt = select(Role).where(Role.name == role_name).execution_options(ignore_tenant=True)
        result = await session.execute(stmt)
        role = result.scalar_one_or_none()
        
        if not role:
            logger.info(f"Role '{role_name}' not found. Creating...")
            new_role = Role(name=role_name, description=f"Default {role_name} role")
            session.add(new_role)
        else:
            logger.debug(f"Role '{role_name}' already exists.")
            
    await session.commit()
    logger.info("Role seeding completed.")
