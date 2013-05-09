class itteam {
	include virt_users, virt_groups

	realize(
		Group["itteam"],
		User["wout"],
		User["jorn"],
		User["jan"]
	)
}
