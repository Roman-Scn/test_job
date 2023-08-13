# test_job
Для работы скрипта, в коде проверяется наличие файла <filename = 'info.json'> в директории скрипта, в секции <#variables> задайте значение переменной в соотвествии с именем вашего файла.
Содержимое файла из задачи:
{
    "hosts": {
        "EU-CLUSTER": {
            "title": "Eu cluster discription",
            "host": "eu1-vm-host",
            "user": "euuser"
        },
        "NA-CLUSTER": {
            "title": "Na cluster description",
            "host": "na1-vm-host",
            "user": "nauser"
        }
    }
}
