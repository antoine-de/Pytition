#!/usr/bin/env python3
import argparse
import os
import sys

def get_parser():
	parser = argparse.ArgumentParser("genpet")
	subparsers = parser.add_subparsers(help='sub-command help', dest="action")
	genorga = subparsers.add_parser("gen_orga", help="create Pytition Organization")
	genorga.add_argument("--orga", "-o", type=str, required=True)
	genusers = subparsers.add_parser("gen_user", help="create Pytition user")
	genusers.add_argument("--username", "-u", type=str, required=True)
	genusers.add_argument("--first-name", "-f", type=str, required=True)
	genusers.add_argument("--last-name", "-l", type=str, required=True)
	genusers.add_argument("--password", "-p", type=str, required=False, default="f00bar")
	join_org = subparsers.add_parser("join_org", help="make a Pytition user join an Organization")
	join_org.add_argument("--orga", "-o", type=str, required=True)
	join_org.add_argument("--user", "-u", type=str, required=True)
	genpet = subparsers.add_parser("generate_petitions", help="Generate petitions")
	genpet.add_argument("--number", "-n", help="petition number", type=int, required=True)
	genpet.add_argument("--orga", "-o", type=str, required=False)
	genpet.add_argument("--user", "-u", type=str, required=False)
	return parser


def main():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pytition.settings")
	import django
	django.setup()
	from petition.models import Petition, Organization, PytitionUser, Permission

	args = get_parser().parse_args()

	if args.action == "join_org":
		username = args.user
		orgname = args.orga
		u = PytitionUser.objects.get(user__username=username)
		org = Organization.objects.get(name=orgname)
		print("user: {}".format(u))
		print("orga: {}".format(org))
		org.members.add(u)
		org.save()
		perms = Permission.objects.create(organization=org)
		perms.can_add_members = True
		perms.can_remove_members = True
		perms.can_create_petitions = True
		perms.can_modify_petitions = True
		perms.can_delete_petitions = True
		perms.can_view_signatures = True
		perms.can_modify_signatures = True
		perms.can_delete_signatures = True
		perms.can_modify_permissions = True
		perms.save()
		u.permissions.add(perms)
		u.save()
	elif args.action == "generate_petitions":
		if args.orga == None and args.user == None:
			print("You must either specify --orga or --user")
			sys.exit(1)
		if args.number:
			for i in range(args.number):
				p = Petition.objects.create(title="Petition"+str(i), text="blabla"+str(i), org_twitter_handle="@RAP_Asso",
											published=True)
				p.save()
				if args.orga:
					orgname = args.orga
					orga = Organization.objects.get(name=orgname)
					orga.petitions.add(p)
					orga.save()
				elif args.user:
					username = args.user
					u = PytitionUser.objects.get(user__username=username)
					u.petitions.add(p)
					u.save()
	elif args.action == "gen_user":
		from django.contrib.auth.models import User
		user = User.objects.create_user(args.username, password=args.password)
		user.is_staff = True
		if args.first_name:
			user.first_name = args.first_name
		if args.last_name:
			user.last_name = args.last_name
		user.save()
	elif args.action == "gen_orga":
		org = Organization.objects.create(name=args.orga)
		org.save()
	else:
		print("You should chose an action, see --help for more information")


if __name__ == "__main__":
	main()
