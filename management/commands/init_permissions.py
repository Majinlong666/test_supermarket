from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from accounts.models import Employee
from sales.models import SalesOrder, SalesOrderItem

class Command(BaseCommand):
    help = '初始化系统角色（Admin/Sales）和测试账号'

    def handle(self, *args, **options):
        # 1. 创建角色组
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ 创建Admin角色组成功'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin角色组已存在'))

        sales_group, created = Group.objects.get_or_create(name='Sales')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ 创建Sales角色组成功'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Sales角色组已存在'))

        # 2. 给Sales组分配销售单相关权限
        try:
            sales_ct = [
                ContentType.objects.get_for_model(SalesOrder),
                ContentType.objects.get_for_model(SalesOrderItem)
            ]
            sales_perms = Permission.objects.filter(content_type__in=sales_ct)
            sales_group.permissions.set(sales_perms)
            self.stdout.write(self.style.SUCCESS('✅ 给Sales组分配权限成功'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ 分配权限失败：{str(e)}'))

        # 3. 创建管理员账号（admin/123456）
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                password='123456',
                email='admin@test.com',
                first_name='管理员',
                last_name='张三'
            )
            # 创建员工信息
            Employee.objects.create(user=admin_user, phone='13800138000')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('✅ 管理员账号创建成功：admin/123456'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ 管理员账号已存在'))

        # 4. 创建销售人员账号（sales/123456）
        if not User.objects.filter(username='sales').exists():
            sales_user = User.objects.create_user(
                username='sales',
                password='123456',
                first_name='销售',
                last_name='李四'
            )
            # 创建员工信息
            Employee.objects.create(user=sales_user, phone='13900139000')
            sales_user.groups.add(sales_group)
            self.stdout.write(self.style.SUCCESS('✅ 销售人员账号创建成功：sales/123456'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ 销售人员账号已存在'))

        self.stdout.write(self.style.SUCCESS('\n🎉 角色和账号初始化完成！'))
