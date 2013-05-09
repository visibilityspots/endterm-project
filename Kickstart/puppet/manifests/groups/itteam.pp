class itteam {
	include virt_users, virt_groups

	realize(
		User["root"],
		Group["itteam"],
		User["wout"],
		User["jan"],
		User["jorn"]
	)
}
