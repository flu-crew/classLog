#Time the training
/usr/bin/time -v classlog train -d "|" -n 1 -p 0.05 classlog/examples/prrsv/annotated_prrsv2.fasta	
/usr/bin/time -v classlog train -d "|" -n 1 -p 0.05 classlog/examples/prrsv/annotated_prrsv1and2.fasta
/usr/bin/time -v classlog train -d "|" -n 2 -p 0.05 classlog/examples/h1_iav/nt/no2020_train.aln.fasta

#Time the prediction
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle classlog/examples/time_trial/unknown_yoon_prrsv.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv1and2.fasta.classify.pickle classlog/examples/time_trial/unknown_yoon_prrsv.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle classlog/examples/time_trial/annotated_prrsv1and2.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv1and2.fasta.classify.pickle classlog/examples/time_trial/annotated_prrsv1and2.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/h1_iav/nt/no2020_train.aln.fasta.classify.pickle classlog/examples/time_trial/2020_test.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/h1_iav/nt/no2020_train.aln.fasta.classify.pickle classlog/examples/time_trial/BVBRC_genome_sequence.fasta -t 0.7


