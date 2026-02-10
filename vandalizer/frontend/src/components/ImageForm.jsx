import { uploadImage } from "../services/api";

export const ImageForm = ({ loading, setLoading, setErr, onSuccess }) => {
    const handleFileChange = async e => {
        if (loading)
            return;

        setLoading(true);
        setErr(null);

        try {
            const res = await uploadImage(e.target.files[0]);
            onSuccess?.(res);
        } catch (err) {
            console.log(err)
            setErr("Failed to upload image, check developer console for details");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <input type='file' accept="image/*" onChange={handleFileChange} />
        </div>
    )
}