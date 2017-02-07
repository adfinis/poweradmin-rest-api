# Add foreign key constraints to existing PowerDNS database 
#
# https://doc.powerdns.com/md/authoritative/backend-generic-mysql/#generic-mysql-backend
#


# Add missing `disabled` column
ALTER TABLE records ADD COLUMN disabled TINYINT(1) DEFAULT 0;


# Delete records if domain does not exist anymore
DELETE records FROM records
LEFT JOIN domains ON domains.id = records.domain_id
WHERE domains.id IS NULL;

ALTER TABLE `records`
ADD CONSTRAINT `fk_records_domains_domain_id`
FOREIGN KEY (`domain_id`)
REFERENCES `domains` (`id`)
ON DELETE CASCADE;


# Delete zones if domain does not exist anymore
DELETE zones FROM zones
LEFT JOIN domains ON domains.id = zones.domain_id
WHERE domains.id IS NULL;

ALTER TABLE `zones`
ADD CONSTRAINT `fk_zones_domain_domain_id`
FOREIGN KEY (`domain_id`)
REFERENCES `domains` (`id`)
ON DELETE CASCADE;
