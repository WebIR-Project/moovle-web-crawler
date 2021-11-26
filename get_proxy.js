(() => {
	const trs = $('#proxylisttable tbody tr').toArray()
	let data = ''
	for (let tr of trs) {
		data += ($(tr).find('td:eq(6)').text() === 'yes' ? 'https://' : 'http://') + $(tr).find('td:eq(0)').text() + ':' + $(tr).find('td:eq(1)').text() + '\n'
	}
	console.log(data)
})()