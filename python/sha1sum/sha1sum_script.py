import hashlib
import os
import sys
import shutil

UPDATED_BLOBS_DIR = "updated_blobs"

def calculate_sha1sum(file_path):
    sha1 = hashlib.sha1()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"[ERRO] Não foi possível calcular SHA-1 de {file_path}: {e}")
        return None


def process_proprietary_files(file_path, vendor_base_dir, check_only=False):
    updated_lines = []
    ok_count, diff_count, missing_count, skipped_count, copied_count = 0, 0, 0, 0, 0

    try:
        with open(file_path, "r") as f:
            for original_line in f:
                line = original_line.strip()

                # Comentários e linhas vazias
                if not line or line.startswith("#"):
                    updated_lines.append(original_line.rstrip("\n"))
                    continue

                # Só processar linhas com hash
                if "|" not in line:
                    skipped_count += 1
                    updated_lines.append(original_line.rstrip("\n"))
                    continue

                blob_path_full, old_hash = line.split("|", 1)

                # Determinar caminhos de origem e destino
                if ":" in blob_path_full:
                    source_path, dest_path = blob_path_full.split(":", 1)
                else:
                    source_path = blob_path_full
                    dest_path = blob_path_full  # destino é igual ao caminho original se não tiver ":"

                absolute_source = os.path.join(vendor_base_dir, source_path)

                if os.path.isfile(absolute_source):
                    sha1sum = calculate_sha1sum(absolute_source)
                    if sha1sum:
                        if sha1sum != old_hash:
                            diff_count += 1
                            if check_only:
                                print(f"[DIFERENTE] {blob_path_full}")
                                updated_lines.append(original_line.rstrip("\n"))
                            else:
                                # Atualiza hash
                                updated_lines.append(f"{blob_path_full}|{sha1sum}")
                                print(f"[ATUALIZADO] {blob_path_full}|{sha1sum}")

                                # Copiar o blob para updated_blobs
                                dest_file = os.path.join(UPDATED_BLOBS_DIR, dest_path)
                                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                                shutil.copy2(absolute_source, dest_file)
                                copied_count += 1
                        else:
                            ok_count += 1
                            if check_only:
                                print(f"[OK] {blob_path_full}")
                            updated_lines.append(original_line.rstrip("\n"))
                else:
                    missing_count += 1
                    print(f"[AVISO] Blob não encontrado: {source_path}")
                    updated_lines.append(original_line.rstrip("\n"))

        if check_only:
            print(f"\nResumo: {ok_count} OK, {diff_count} diferentes, {missing_count} não encontrados, {skipped_count} ignorados (sem hash).")
        else:
            temp_file = file_path + ".new"
            with open(temp_file, "w") as f:
                f.write("\n".join(updated_lines) + "\n")

            # Substituir o arquivo original
            shutil.move(temp_file, file_path)

            print(f"\n[OK] Arquivo '{file_path}' atualizado com sucesso.")
            print(f"Resumo: {ok_count} OK, {diff_count} atualizados, {missing_count} não encontrados, {skipped_count} ignorados (sem hash), {copied_count} blobs copiados para '{UPDATED_BLOBS_DIR}'.")

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{file_path}' não encontrado.")
    except Exception as e:
        print(f"[ERRO] Problema ao processar '{file_path}': {e}")


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    proprietary_files_path = os.path.join(base_path, "proprietary-files.txt")

    if len(sys.argv) < 3:
        print("Uso:")
        print("  python update_sha1.py --update <caminho_para_vendor>")
        print("  python update_sha1.py --check <caminho_para_vendor>")
        sys.exit(1)

    mode = sys.argv[1]
    vendor_base_dir = sys.argv[2]

    print(f"Arquivo proprietary-files.txt: {proprietary_files_path}")
    print(f"Pasta base (vendor) especificada: {vendor_base_dir}\n")

    if mode == "--update":
        process_proprietary_files(proprietary_files_path, vendor_base_dir, check_only=False)
    elif mode == "--check":
        process_proprietary_files(proprietary_files_path, vendor_base_dir, check_only=True)
    else:
        print("[ERRO] Modo inválido! Use --update ou --check.")


if __name__ == "__main__":
    main()
